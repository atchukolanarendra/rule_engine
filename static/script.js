document.getElementById("create_rule_btn").onclick = function() {
    const ruleString = document.getElementById("rule_string").value;

    fetch('/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_string: ruleString })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = "Rule created: " + JSON.stringify(data);
    })
    .catch(error => {
        document.getElementById("output").innerText = "Error: " + error;
    });
};

document.getElementById("combine_rule_btn").onclick = function() {
    const rule1 = document.getElementById("combine_rule1").value;
    const rule2 = document.getElementById("combine_rule2").value;

    fetch('/combine_rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rules: [rule1, rule2] })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = "Combined rule: " + JSON.stringify(data);
    })
    .catch(error => {
        document.getElementById("output").innerText = "Error: " + error;
    });
};

document.getElementById("evaluate_rule_btn").onclick = function() {
    const ruleId = document.getElementById("evaluate_rule_id").value;
    const userData = document.getElementById("user_data").value;

    fetch('/evaluate_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            rule_id: ruleId,
            user_data: JSON.parse(userData)
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = "Evaluation result: " + data.result;
    })
    .catch(error => {
        document.getElementById("output").innerText = "Error: " + error;
    });
};
