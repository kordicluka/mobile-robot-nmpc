import casadi as ca
from acados_template import AcadosModel


def create_unicycle_model() -> AcadosModel:
    model = AcadosModel()
    model.name = "unicycle"

    x     = ca.SX.sym("x")
    y     = ca.SX.sym("y")
    theta = ca.SX.sym("theta")
    v     = ca.SX.sym("v")
    omega = ca.SX.sym("omega")

    dv    = ca.SX.sym("dv")
    domega = ca.SX.sym("domega")

    model.x = ca.vertcat(x, y, theta, v, omega)
    model.u = ca.vertcat(dv, domega)

    model.f_expl_expr = ca.vertcat(
        v * ca.cos(theta),
        v * ca.sin(theta),
        omega,
        dv,
        domega,
    )

    return model
