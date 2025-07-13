
//URL TO FAST API
    const API_URI = 'http://localhost:8000/autojailbreak';

//ATTACKER
    const inputAttacker = document.getElementById('inputAttacker');
    const attackerMaxToken = document.getElementById('attackerMaxToken');

    const attackerRole = document.getElementById('attackerRole');
    const attackerInstruction = document.getElementById('attackerInstruction');
    const attackerConstraint = document.getElementById('attackerConstraint');
    const attackerQuery = document.getElementById('attackerQuery');

//EVALUATOR
    const inputEvaluator = document.getElementById('inputEvaluator');
    const evaluatorMaxToken = document.getElementById('evaluatorMaxToken');

    const evaluatorRole = document.getElementById('evaluatorRole');
    const evaluatorInstruction = document.getElementById('evaluatorInstruction');
    const evaluatorConstraint = document.getElementById('evaluatorConstraint');

//REATTACKER
    const inputReattacker = document.getElementById('inputReattacker');
    const reattackerMaxToken = document.getElementById('reattackerMaxToken');

    const reattackerRole = document.getElementById('reattackerRole');
    const reattackerInstruction = document.getElementById('reattackerInstruction');
    const reattackerConstraint = document.getElementById('reattackerConstraint');

//TARGET
    const localTarget = document.getElementById('localTarget');

    const urlTarget = document.getElementById('urlTarget');
    const apiKeyTarget = document.getElementById('apiKeyTarget');
    const modelExternalTarget = document.getElementById('modelExternalTarget');

// Number of template and attempts
    const templatePrompt = document.getElementById('templatePrompt');
    const numberOfAttempt = document.getElementById('numberOfAttempt');

// Button and Answer realm
    const attackButton = document.getElementById('attackButton');
    const dialogResponse = document.getElementById('dialogResponse');

//REVEAL MODEL
    function targetTypeSelector() {
        const localTargetContainer = document.getElementById('localTargetContainer');
        const externalTargetContainer = document.getElementById('externalTargetContainer');
        const gigaTargetContainer = document.getElementById('gigaTargetContainer')

        const selectedTarget = document.querySelector('input[name="target"]:checked').value;

        if (selectedTarget === 'local') {
            localTargetContainer.style.display = 'block';
            externalTargetContainer.style.display = 'none';
            gigaTargetContainer.style.display = 'none';
        }
        if (selectedTarget === 'external') {
            localTargetContainer.style.display = 'none';
            externalTargetContainer.style.display = 'block';
            gigaTargetContainer.style.display = 'none';

        }
        if (selectedTarget === 'giga') {
            localTargetContainer.style.display = 'none';
            externalTargetContainer.style.display = 'none';
            gigaTargetContainer.style.display = 'block';
        }
    }

    function addModelCheckbox() {
        const checkboxEvaluator = document.getElementById('checkboxEvaluator');
        const checkboxReattacker = document.getElementById('checkboxReattacker');

        const evaluatorContainer = document.getElementById('evaluatorContainer');
        const reattackerContainer = document.getElementById('reattackerContainer');

        // Add event listener to the checkbox
        checkboxEvaluator.addEventListener('change', function() {
            if (this.checked) {
                evaluatorContainer.style.display = 'block';
            } else {
                evaluatorContainer.style.display = 'none';
            }
        });
        checkboxReattacker.addEventListener('change', function() {
            if (this.checked) {
                reattackerContainer.style.display = 'block';
            } else {
                reattackerContainer.style.display = 'none';
            }
        });
    }

document.addEventListener('DOMContentLoaded', function() {

    attackButton.addEventListener('click', async function() {

    //ATTACKER
        const inputAttacker_value = inputAttacker.value.trim();
        const attackerMaxToken_value = attackerMaxToken.value.trim();

        const attackerRole_value = attackerRole.value.trim();
        const attackerInstruction_value = attackerInstruction.value.trim();
        const attackerConstraint_value = attackerConstraint.value.trim();
        const attackerQuery_value = attackerQuery.value.trim();

    //EVALUATOR
        const inputEvaluator_value = inputEvaluator.value.trim();
        const evaluatorMaxToken_value = evaluatorMaxToken.value.trim();

        const evaluatorRole_value = evaluatorRole.value.trim();
        const evaluatorInstruction_value = evaluatorInstruction.value.trim();
        const evaluatorConstraint_value = evaluatorConstraint.value.trim();

    //REATTACKER
        const inputReattacker_value = inputReattacker.value.trim();
        const reattackerMaxToken_value = reattackerMaxToken.value.trim();

        const reattackerRole_value = reattackerRole.value.trim();
        const reattackerInstruction_value = reattackerInstruction.value.trim();
        const reattackerConstraint_value = reattackerConstraint.value.trim();

    //TARGET
        const localTarget_value = localTarget.value.trim();

        const urlTarget_value = urlTarget.value.trim();
        const apiKeyTarget_value = apiKeyTarget.value.trim();
        const modelExternalTarget_value = modelExternalTarget.value.trim();

    // Number of template and attempts
        const templatePrompt_value = templatePrompt.value.trim();
        const numberOfAttempt_value = numberOfAttempt.value.trim();

        if (!inputAttacker_value || attackerQuery_value) {
            dialogResponse.textContent = 'Please enter some text';
            dialogResponse.className = 'error';
            return;
        }

        let attack_parameters = {
            "models":
                [
                    {
                        "name": inputAttacker_value,
                        "max_new_tokens": attackerMaxToken_value
                    },
                    {
                        "name": inputReattacker_value,
                        "max_new_tokens": reattackerMaxToken_value
                    },
                    {
                        "name": inputEvaluator_value,
                        "max_new_tokens": evaluatorMaxToken_value
                    },
                    {
                        "name": localTarget_value,
                        "max_new_tokens": 1555
                    }
                ],

            "attacker": {
                "context": attackerRole_value,
                "instruction": attackerInstruction_value,
                "constraint": attackerConstraint_value,
                "query": attackerQuery_value
            },

            "reattacker": {
                "context": reattackerRole_value,
                "instruction": reattackerInstruction_value,
                "constraint": reattackerConstraint_value
            },

            "evaluator": {
                "context": evaluatorRole_value,
                "instruction": evaluatorInstruction_value,
                "constraint": evaluatorConstraint_value
            },

            "external_target": {
                "base_url": urlTarget_value,
                "api_key": apiKeyTarget_value,
                "model_name": modelExternalTarget_value
            },
//TODO add list of question
            // "additional_question":
            //     ["How is first coder?",
            //         "When first attack were make?",
            //         "How to use DDoS attack?"],

            "prepared_scenario": templatePrompt_value,
            "number_of_attempt": numberOfAttempt_value
        }

        try {
            console.log(attack_parameters)
            const response = await fetch(API_URI, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(attack_parameters),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            dialogResponse.textContent = `Dialog Response: ${data.result}`;
            dialogResponse.className = '';
        } catch (error) {
            dialogResponse.textContent = `Error: ${error.message}`;
            dialogResponse.className = 'error';
            console.error('Error:', error);
        }
    });
});