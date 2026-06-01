import os
import ctypes
import numpy as np
import yaml

if "ACADOS_SOURCE_DIR" not in os.environ:
    os.environ["ACADOS_SOURCE_DIR"] = os.path.expanduser("~/Documents/fer/acados")

_lib_dir = os.path.join(os.environ["ACADOS_SOURCE_DIR"], "lib")
for _lib in ["libblasfeo.so", "libhpipm.so", "libacados.so"]:
    _p = os.path.join(_lib_dir, _lib)
    if os.path.exists(_p):
        ctypes.CDLL(_p, mode=ctypes.RTLD_GLOBAL)

from acados_template import AcadosOcp, AcadosOcpSolver
from src.model import create_unicycle_model


def load_params(path="config/params.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def create_solver(obstacles: list[tuple] = []) -> AcadosOcpSolver:
    p = load_params()
    mpc = p["mpc"]
    env = p["environment"]
    robot = p["robot"]

    N = mpc["N"]
    dt = mpc["dt"]
    Q = np.diag(mpc["Q"])
    R = np.diag(mpc["R"])

    ocp = AcadosOcp()
    ocp.model = create_unicycle_model()

    nx = 5
    nu = 2
    ny = 3 + nu

    ocp.solver_options.N_horizon = N

    ocp.cost.cost_type = "LINEAR_LS"
    ocp.cost.cost_type_e = "LINEAR_LS"

    ocp.cost.Vx = np.zeros((ny, nx))
    ocp.cost.Vx[:3, :3] = np.eye(3)

    ocp.cost.Vu = np.zeros((ny, nu))
    ocp.cost.Vu[3:, :] = np.eye(nu)

    ocp.cost.Vx_e = np.zeros((3, nx))
    ocp.cost.Vx_e[:3, :3] = np.eye(3)

    ocp.cost.W   = np.block([[Q, np.zeros((3, nu))],
                              [np.zeros((nu, 3)), R]])
    ocp.cost.W_e = Q

    ocp.cost.yref   = np.zeros(ny)
    ocp.cost.yref_e = np.zeros(3)

    ocp.constraints.lbu = np.array([-robot["dv_max"], -robot["domega_max"]])
    ocp.constraints.ubu = np.array([ robot["dv_max"],  robot["domega_max"]])
    ocp.constraints.idxbu = np.array([0, 1])

    ocp.constraints.lbx = np.array([env["x_min"], env["y_min"], -np.pi,
                                     robot["v_min"], -robot["omega_max"]])
    ocp.constraints.ubx = np.array([env["x_max"], env["y_max"],  np.pi,
                                     robot["v_max"],  robot["omega_max"]])
    ocp.constraints.idxbx = np.array([0, 1, 2, 3, 4])

    ocp.constraints.lbx_e = ocp.constraints.lbx.copy()
    ocp.constraints.ubx_e = ocp.constraints.ubx.copy()
    ocp.constraints.idxbx_e = ocp.constraints.idxbx.copy()

    if obstacles:
        _add_obstacle_constraints(ocp, obstacles, robot["radius"], mpc["constraints"])

    ocp.constraints.x0 = np.zeros(nx)

    ocp.solver_options.tf = N * dt
    ocp.solver_options.integrator_type = "ERK"
    ocp.solver_options.nlp_solver_type = mpc["solver_type"]
    ocp.solver_options.qp_solver = "PARTIAL_CONDENSING_HPIPM"
    ocp.solver_options.hessian_approx = "GAUSS_NEWTON"
    ocp.solver_options.nlp_solver_max_iter = 50

    os.makedirs(".acados_build", exist_ok=True)
    solver = AcadosOcpSolver(ocp, json_file=".acados_build/acados_ocp.json")
    return solver


def _add_obstacle_constraints(ocp, obstacles, r_robot, constraint_type):
    import casadi as ca

    x = ocp.model.x
    px, py = x[0], x[1]

    h_list = []
    for (cx, cy, r) in obstacles:
        h_list.append((px - cx)**2 + (py - cy)**2 - (r + r_robot)**2)

    ocp.model.con_h_expr = ca.vertcat(*h_list)
    ocp.model.con_h_expr_e = ca.vertcat(*h_list)

    n_obs = len(obstacles)
    ocp.constraints.lh = np.zeros(n_obs)
    ocp.constraints.uh = np.ones(n_obs) * 1e6
    ocp.constraints.lh_e = np.zeros(n_obs)
    ocp.constraints.uh_e = np.ones(n_obs) * 1e6

    if constraint_type == "soft":
        ocp.constraints.idxsh = np.arange(n_obs)
        ocp.constraints.idxsh_e = np.arange(n_obs)
        penalty = 1e4
        ocp.cost.zl = penalty * np.ones(n_obs)
        ocp.cost.zu = penalty * np.ones(n_obs)
        ocp.cost.Zl = penalty * np.ones(n_obs)
        ocp.cost.Zu = penalty * np.ones(n_obs)
        ocp.cost.zl_e = penalty * np.ones(n_obs)
        ocp.cost.zu_e = penalty * np.ones(n_obs)
        ocp.cost.Zl_e = penalty * np.ones(n_obs)
        ocp.cost.Zu_e = penalty * np.ones(n_obs)
