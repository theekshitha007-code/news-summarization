const newsInput = document.getElementById("newsInput");
const charCount = document.getElementById("charCount");
const charWarning = document.getElementById("charWarning");
const summaryBox = document.getElementById("summary");
const loading = document.getElementById("loading");
const summarizeBtn = document.getElementById("summarizeBtn");

const MAX_CHARACTERS = 10000;


// Live character counter

newsInput.addEventListener("input", function () {

    const currentLength = newsInput.value.length;

    charCount.textContent =
        currentLength.toLocaleString() +
        " / 10,000 characters";


    // Warning messages

    if (currentLength >= MAX_CHARACTERS) {

        charWarning.textContent =
            "Maximum 10,000 characters reached.";

    }

    else if (currentLength >= 9000) {

        charWarning.textContent =
            "You are close to the 10,000-character limit.";

    }

    else {

        charWarning.textContent = "";

    }

});


// Summarize News

async function summarizeNews() {

    const news = newsInput.value.trim();


    // Empty input check

    if (news === "") {

        alert("Please enter a news article.");

        return;
    }


    // Character limit check

    if (news.length > MAX_CHARACTERS) {

        alert("Please enter a maximum of 10,000 characters.");

        return;
    }


    // Show loading

    loading.style.display = "flex";

    summarizeBtn.disabled = true;

    summaryBox.textContent =
        "Generating summary...";


    try {

        const response = await fetch("/summarize", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                news: news
            })

        });


        if (!response.ok) {

            throw new Error(
                "Server error: " + response.status
            );

        }


        const data = await response.json();


        // Display summary

        summaryBox.textContent =
            data.summary || "No summary generated.";

    }


    catch (error) {

        console.error(error);

        summaryBox.textContent =
            "Something went wrong. Please check the Flask terminal.";

    }


    finally {

        loading.style.display = "none";

        summarizeBtn.disabled = false;

    }

}


// Clear button

function clearText() {

    newsInput.value = "";

    charCount.textContent =
        "0 / 10,000 characters";

    charWarning.textContent = "";

    summaryBox.textContent =
        "Your summary will appear here.";

    loading.style.display = "none";

    summarizeBtn.disabled = false;

}