import entity_table
import model_output
import model_input

class DatabaseService:

    def __init__(self, database_instance):
        self.database_instance = database_instance

    def get_dialog_by_id(self, param_id: int):
        return self.database_instance.query(entity_table.Dialog).filter(entity_table.Dialog.id == param_id).first()

    def get_dialogs(self, skip: int = 0, limit: int = 100):
        return self.database_instance.query(entity_table.Dialog).offset(skip).limit(limit).all()

    def add_dialog(self, dialog_out: model_output.Dialog):
        db_dialog = entity_table.Dialog(
            dialog = dialog_out.dialog,
        )
        self.database_instance.add(db_dialog)
        self.database_instance.commit()
        self.database_instance.refresh(db_dialog)


    def get_attack_parameter_by_id(self, param_id: int):
        return self.database_instance.query(entity_table.AttackerParameters).filter(entity_table.AttackerParameters.id == param_id).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.database_instance.query(entity_table.AttackerParameters).offset(skip).limit(limit).all()

    def add_attack_parameter(self, attacker_parameter: model_input.AttackerParameters):
        db_attacker_parameters = entity_table.AttackerParameters(
            attacker = attacker_parameter.attacker,
            max_token_attacker = attacker_parameter.max_token_attacker,

            attacker_role=attacker_parameter.attacker_role,
            attacker_instruction=attacker_parameter.attacker_instruction,
            attacker_constraint=attacker_parameter.attacker_constraint,
            attacker_query=attacker_parameter.attacker_query,

            evaluator=attacker_parameter.evaluator,
            max_token_evaluator=attacker_parameter.max_token_evaluator,

            evaluator_role=attacker_parameter.evaluator_role,
            evaluator_instruction=attacker_parameter.evaluator_instruction,
            evaluator_constraint=attacker_parameter.evaluator_constraint,

            reattacker=attacker_parameter.reattacker,
            max_token_reattacker=attacker_parameter.max_token_reattacker,

            reattacker_role=attacker_parameter.reattacker_role,
            reattacker_instruction=attacker_parameter.reattacker_instruction,
            reattacker_constraint=attacker_parameter.reattacker_constraint,

            local_target=attacker_parameter.local_target,

            url_external_target=attacker_parameter.url_external_target,
            apikey_external_target=attacker_parameter.apikey_external_target,
            model_external_target=attacker_parameter.model_external_target,

            uuid_external_target=attacker_parameter.uuid_external_target,
            authorization_external_target=attacker_parameter.authorization_external_target,

            template_prompt=attacker_parameter.template_prompt,
            number_attempt=attacker_parameter.number_attempt,

        )

        self.database_instance.add(db_attacker_parameters)
        self.database_instance.commit()
        self.database_instance.refresh(db_attacker_parameters)
