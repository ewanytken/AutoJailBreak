
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

// Giga
    const uuidTarget = document.getElementById("uuidTarget");
    const authorizationTarget = document.getElementById("authorizationTarget");

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
    function displayJsonResponse(jsonData) {

        const responseDiv = document.getElementById('dialogResponse');
        let html = '<div class="json-container">';
        const groups = {};

        Object.entries(jsonData).forEach(([key, value]) => {
            const groupNum = key.match(/\d+$/)?.[0] || '0';

            if (!groups[groupNum]) groups[groupNum] = [];

            groups[groupNum].push({ key, value });
        });

        Object.entries(groups).forEach(([groupNum, items]) => {
            html += `<div class="json-group" data-group="ATTEMPT ${groupNum}">`;

            items.forEach(item => {
                html += `
                <div class="json-item">
                    <span class="json-key">"${item.key}"</span>
                    <span class="json-value">"${item.value.trim()}"</span>
                </div>
                `;
            });
            html += '</div>';
        });

      html += '</div>';

      responseDiv.innerHTML = html;
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

    //Giga
        const uuidTarget_value = uuidTarget.value.trim();
        const authorizationTarget_value = authorizationTarget.value.trim();

    // Number of template and attempts
        const templatePrompt_value = templatePrompt.value.trim();
        const numberOfAttempt_value = numberOfAttempt.value.trim();

        if (!inputAttacker_value || !attackerQuery_value) {
            dialogResponse.textContent = 'Please enter Attack model and Attacks tunes';
            dialogResponse.className = 'error';
            return;
        }

        if (!localTarget_value && !urlTarget_value && !uuidTarget_value) {
            dialogResponse.textContent = 'Please enter Attack model, Attacks tunes and Target Model';
            dialogResponse.className = 'error';
            return;
        }

        let attack_parameters = {"models": []};

        if (inputAttacker_value !== '') {
            attack_parameters["models"].push({"name": inputAttacker_value,
                                              "max_new_tokens": Number(attackerMaxToken_value)});

            attack_parameters.attacker = {};

            attack_parameters.attacker.context = attackerRole_value ?? "None";
            attack_parameters.attacker.instruction = attackerInstruction_value ?? "None";
            attack_parameters.attacker.constraint = attackerConstraint_value ?? "None";
            attack_parameters.attacker.query = attackerQuery_value;
        }

        if (inputReattacker_value !== '') {
            attack_parameters["models"].push({"name": inputReattacker_value,
                                              "max_new_tokens": Number(reattackerMaxToken_value)});

            attack_parameters.reattacker = {};

            attack_parameters.reattacker.context = reattackerRole_value ?? "None";
            attack_parameters.reattacker.instruction = reattackerInstruction_value ?? "None";
            attack_parameters.reattacker.constraint = reattackerConstraint_value ?? "None";
        }

        if (inputEvaluator_value !== '') {
            attack_parameters["models"].push({"name": inputEvaluator_value,
                                              "max_new_tokens": Number(evaluatorMaxToken_value)});

            attack_parameters.evaluator = {};

            attack_parameters.evaluator.context = evaluatorRole_value ?? "None";
            attack_parameters.evaluator.instruction = evaluatorInstruction_value ?? "None";
            attack_parameters.evaluator.constraint = evaluatorConstraint_value ?? "None";
       }

        try {
            if (localTarget_value !== '') {
                attack_parameters["models"].push({"name": localTarget_value});
            }
            else if ((urlTarget_value || uuidTarget_value) !== '') {
                attack_parameters.external_target = {}
                if ((urlTarget_value && apiKeyTarget_value && modelExternalTarget_value) !== '') {
                    attack_parameters.external_target.base_url = urlTarget_value;
                    attack_parameters.external_target.api_key = apiKeyTarget_value;
                    attack_parameters.external_target.model_name = modelExternalTarget_value;
                }
                else if ((uuidTarget_value && authorizationTarget_value) !== ''){
                    attack_parameters.external_target.authorization = authorizationTarget_value;
                    attack_parameters.external_target.uuid = uuidTarget_value;
                }
                else {
                    throw new Error("External model assignment ERROR");
                }
            }
            else{
                throw new Error("Target Model assignment ERROR");
            }
        } catch (error) {
            console.error('Target Model assignment ERROR: ', error);
        }

        if (templatePrompt_value !== '') {
            attack_parameters.prepared_scenario = Number(templatePrompt_value);
        }
        if (numberOfAttempt_value !== '') {
            attack_parameters.number_of_attempt = Number(numberOfAttempt_value);
        }

        try {
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

            // dialogResponse.textContent = `Dialog Response: ${data.result}`; old option

            displayJsonResponse(data.result)
            dialogResponse.className = '';

        } catch (error) {
            dialogResponse.textContent = `Error: ${error.message}`;
            dialogResponse.className = 'error';
            console.error('Error:', error);
        }
    });
});