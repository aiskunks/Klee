from klee_engine.api import route_utils

experiment_module = route_utils.DBConstraintErrorHandler(
    db_constraint_name="unique_module_for_experiment",
    field_name="module_name",
    message="Pipeline Module is already created for this experiment",
)

experiment_module_fk = route_utils.DBConstraintErrorHandler(
    db_constraint_name="experiment_module_pipeline_module_id_fkey",
    field_name="module_name",
    message="There is no Pipeline Module with a provided `module_name`",
)

user_email_key = route_utils.DBConstraintErrorHandler(
    db_constraint_name="users_email_key",
    field_name="email",
    message="User with this email already exists",
)

wrong_email = route_utils.DBConstraintErrorHandler(
    db_constraint_name="user_not_found",
    field_name="email",
    message="Email not found"
)

wrong_password = route_utils.DBConstraintErrorHandler(
    db_constraint_name="wrong_password",
    field_name="password",
    message="Wrong Password",
)

