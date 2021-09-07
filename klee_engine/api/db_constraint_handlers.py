from klee_engine.api import route_utils

experiment_module = route_utils.DBConstraintErrorHandler(
    db_constraint_name="unique_module_for_experiment",
    field_name="pipeline_module_id",
    message="Pipeline Module is already created for this experiment",
)

experiment_module_fk = route_utils.DBConstraintErrorHandler(
    db_constraint_name="experiment_module_pipeline_module_id_fkey",
    field_name="pipeline_module_id",
    message="There is no Pipeline Module with a provided `pipeline_module_id`",
)
