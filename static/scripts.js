let score = 0;

$(document).ready(() => {
    $("#start").click(() => {
        const role = $("#role").val();
        if (!role) {
            alert("Please enter a job role.");
            return;
        }

        // Start the interview and fetch the first question
        fetchQuestion(role);
        $("#role-section").addClass("hidden");
        $("#question-section").removeClass("hidden");
    });

    $("#submit-answer").click(() => {
        const question = $("#question").text();
        const userAnswer = $("#answer").val();
        if (!userAnswer) {
            alert("Please provide an answer.");
            return;
        }

        // Validate the answer
        fetch("/api/answer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, answer: userAnswer })
        })
        .then(response => response.json())
        .then(data => {
            const correctAnswer = data.answer;
            const isCorrect = data.correct;
            if (isCorrect) {
                score += 10;
                $("#feedback-section").text("Correct! +10 Points.");
            } else {
                score -= 4;
                $("#feedback-section").text(`Incorrect. The correct answer is: ${correctAnswer}. -4 Points.`);
            }
            $("#score").text(score);
            fetchQuestion($("#role").val());
        });
    });

    $("#hint").click(() => {
        const question = $("#question").text();

        fetch("/api/hint", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        })
        .then(response => response.json())
        .then(data => {
            const hint = data.hint;
            $("#hint-text").text(`Hint: ${hint}`);
            score -= 5;
            $("#score").text(score);
        });
    });
});

function fetchQuestion(role) {
    fetch("/api/question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        const question = data.question;
        $("#question").text(question);
        $("#answer").val("");
        $("#hint-text").text("");
    });
}
