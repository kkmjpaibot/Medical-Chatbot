let step = 0;
let userData = {};

const chat = document.getElementById("chat");
const input = document.getElementById("userInput");

/* ---------------- MESSAGE HELPERS ---------------- */
async function showTypingIndicator(duration = 3000) {
    const typing = document.createElement("div");
    typing.className = "message bot typing";
    typing.innerText = "Erica is typing...";
    chat.appendChild(typing);
    chat.scrollTop = chat.scrollHeight;

    return new Promise((resolve) => {
        setTimeout(() => {
            typing.remove();
            resolve();
        }, duration);
    });
}

async function bot(msg, delay = 400) {
    await showTypingIndicator(3000);
    return new Promise((resolve) => {
        setTimeout(() => {
            chat.innerHTML += `<div class="message bot">${msg}</div>`;
            chat.scrollTop = chat.scrollHeight;
            resolve();
        }, delay);
    });
}

function user(msg) {
    chat.innerHTML += `<div class="message user">${msg}</div>`;
    chat.scrollTop = chat.scrollHeight;
}

/* ---------------- PREMIUM TABLE ---------------- */
const premiumTable = {
    18: { comprehensive: 113.00, basic: 93.00 },
    19: { comprehensive: 113.00, basic: 93.00 },
    20: { comprehensive: 113.00, basic: 93.00 },
    21: { comprehensive: 113.00, basic: 93.00 },
    22: { comprehensive: 123.00, basic: 103.00 },
    23: { comprehensive: 123.00, basic: 103.00 },
    24: { comprehensive: 123.00, basic: 103.00 },
    25: { comprehensive: 123.00, basic: 103.00 },
    26: { comprehensive: 133.00, basic: 113.00 },
    27: { comprehensive: 133.00, basic: 113.00 },
    28: { comprehensive: 133.00, basic: 113.00 },
    29: { comprehensive: 133.00, basic: 113.00 },
    30: { comprehensive: 133.00, basic: 113.00 },
    31: { comprehensive: 143.00, basic: 123.00 },
    32: { comprehensive: 143.00, basic: 123.00 },
    33: { comprehensive: 143.00, basic: 123.00 },
    34: { comprehensive: 152.78, basic: 132.78 },
    35: { comprehensive: 154.53, basic: 134.53 },
    36: { comprehensive: 158.08, basic: 138.08 },
    37: { comprehensive: 160.92, basic: 140.92 },
    38: { comprehensive: 162.68, basic: 142.68 },
    39: { comprehensive: 164.10, basic: 144.10 },
    40: { comprehensive: 167.93, basic: 147.93 },
    41: { comprehensive: 179.67, basic: 159.67 },
    42: { comprehensive: 185.92, basic: 165.92 },
    43: { comprehensive: 191.17, basic: 171.17 },
    44: { comprehensive: 198.63, basic: 178.63 },
    45: { comprehensive: 200.47, basic: 180.47 },
    46: { comprehensive: 215.00, basic: 195.00 },
    47: { comprehensive: 221.33, basic: 201.33 },
    48: { comprehensive: 233.33, basic: 213.33 },
    49: { comprehensive: 238.50, basic: 218.50 },
    50: { comprehensive: 250.19, basic: 230.19 },
    51: { comprehensive: 277.38, basic: 257.38 },
    52: { comprehensive: 300.48, basic: 280.48 },
    53: { comprehensive: 314.50, basic: 294.50 },
    54: { comprehensive: 329.27, basic: 309.27 },
    55: { comprehensive: 329.27, basic: 309.27 },
    56: { comprehensive: 329.27, basic: 309.27 },
    57: { comprehensive: 329.27, basic: 309.27 },
    58: { comprehensive: 392.63, basic: 372.63 },
    59: { comprehensive: 428.02, basic: 408.02 },
    60: { comprehensive: 428.02, basic: 408.02 },
    61: { comprehensive: 428.02, basic: 408.02 },
    62: { comprehensive: 428.02, basic: 408.02 },
    63: { comprehensive: 664.67, basic: 644.67 },
    64: { comprehensive: 769.38, basic: 749.38 }
};

/* ---------------- START ---------------- */
function start() {
    bot("👋 Hello, I’m <b>Erica</b>, your Super Agent that will guide you.");
    bot("May I know your name?");
}

/* ---------------- SEND MESSAGE ---------------- */
function sendMessage() {
    if (input.disabled) return; 
    const text = input.value.trim();
    if (!text) return;

    user(text);
    input.value = "";

    // ---------- Step 0: Name ----------
    if (step === 0) {
        userData.name = text;
        bot(`Hello <b>${text}</b>, let’s get to know you better.`);
        bot("May I know your <b>Date of Birth</b>? (DD/MM/YYYY)");
        step = 1;
        return;
    }

    // ---------- Step 1: DOB ----------
    if (step === 1) {
        fetch("/validate_dob", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ dob: text })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "ok") {
                userData.dob = text;
                userData.age = data.age;
                bot(`<b>${data.age}</b> is a great time to plan ahead for your healthcare and medical needs.`);
                step = 2;
                askCoverage();
            } else {
                bot("❌ Invalid format of Date of Birth. Please use <b>DD/MM/YYYY</b>.");
            }
        });
        return;
    }

    // ---------- Step 4: Phone ----------
    if (step === 4) {
        fetch("/validate_phone", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ phone: text })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "ok") {
                userData.phone = text;
                bot("Please type your <b>Email Address</b>.");
                bot("We will send you an email summary of our conversation for your reference.");
                step = 5;
            } else {
                bot("❌ Invalid Malaysian phone number.");
            }
        });
        return;
    }

    // ---------- Step 5: Email ----------
    if (step === 5) {
        fetch("/validate_email", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: text })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "ok") {
                userData.email = text;
                step = 6;
                showFinalSummary();
            } else {
                bot("❌ Invalid email format.");
            }
        });
        return;
    }
}

/* ---------------- TABUNG PERUBATAN INFO ---------------- */
async function showTabungInfo(followWithCoverage = true) {
    await bot(`
        <b>🩺 What is Tabung Perubatan?</b><br><br>
        It's your personal financial safety net for healthcare. Think of it as a <b>Medical Card</b> that gives you:<br><br>

        • <b>Cashless Hospital Admission</b><br>
        Walk into any of our panel hospitals and focus on recovery. No large upfront payments.<br><br>

        • <b>High Annual Limit</b><br>
        Coverage from RM 180,000 to over RM 1,000,000 per year for surgeries, ICU, room & board, and medication.<br><br>

        • <b>Protection for Your Savings</b><br>
        Shields your family’s finances from the shock of a major medical event.
    `);
    if (followWithCoverage) {
        askCoverage();
    }
}

/* ---------------- COVERAGE ---------------- */
async function askCoverage() {
    await bot("Can you tell us about your current protection coverage?");
    showOptions([
        "No coverage at all",
        "Basic employee coverage",
        "Some personal coverage",
        "Comprehensive coverage"
    ], choice => {
        userData.coverage = choice;
        askBudget();
    });
}

/* ---------------- BUDGET ---------------- */
async function askBudget() {
    await bot("How much would you like to spend monthly on your protection plan?");
    showOptions([
        "Less than RM 200",
        "RM 201 - RM 500",
        "RM 500 - RM 1000",
        "More than RM 1000"
    ], choice => {
        userData.budget = choice;
        bot("Please enter your <b>phone number</b> so we can provide you with updates.");
        step = 4;
    });
}

/* ---------------- COVERAGE LEVEL & PREMIUM ---------------- */
async function askCoverageLevel() {
    await bot("Please select your preferred coverage level from the options below:");
    showOptions([
        "BASIC( RM 180,000 / year)",
        "COMPREHENSIVE (RM 1,000,000 /year)"
    ], choice => {
        const age = userData.age;
        let monthlyPremium = 0;

        userData.plan = choice;

        if (premiumTable[age]) {
            monthlyPremium = choice.startsWith("BASIC") ? premiumTable[age].basic : premiumTable[age].comprehensive;
        } else {
            monthlyPremium = choice.startsWith("BASIC") ? 100 : 150; // fallback
        }

        userData.premium = monthlyPremium.toFixed(2);

        bot(`Great! For this coverage level, your estimated monthly premium would be <b>RM ${userData.premium}</b>.`);
        askLearnMore();
    });
}

/* ---------------- LEARN MORE ---------------- */
async function askLearnMore() {
    await bot("Would you like to find out more on how you can be best protected?");
    showOptions([
        "Yes, please",
        "Not now"
    ], () => {
        endChat();
    });
}

/* ---------------- FINAL SUMMARY & SAVE ---------------- */
async function showFinalSummary() {
    await showTabungInfo(false); // show Tabung info without re-running coverage question
    await askCoverageLevel(); // show plan options
}

/* ---------------- END CHAT ---------------- */
async function endChat() {
    input.disabled = true;

    // Send session data to Flask -> Google Sheets
    fetch("/save_session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
    });

    await bot(`
    💖 <b>Great! Thank you for signing up.</b><br>
    We will contact you soon 😊<br><br>
    <small>
    Subject to terms and conditions of approved policy after recommendation by authorised representatives.
    </small>
    `);

    await bot(`
    📞 <b>Contact us:</b> 
    <a href="https://wa.me/60168357258" target="_blank">016-835-7258 (WhatsApp)</a><br>
    Feel free to reach out if you would like more information.
    `);

    // Add Restart Button
    const restartBtn = document.createElement("button");
    restartBtn.innerText = "🔄 Restart Chat";
    restartBtn.className = "restart-btn";
    restartBtn.onclick = () => restartChat();
    chat.appendChild(restartBtn);
    chat.scrollTop = chat.scrollHeight;
}

/* ---------------- RESTART CHAT ---------------- */
function restartChat() {
    chat.innerHTML = "";
    step = 0;
    userData = {};
    input.disabled = false;
    input.value = "";
    input.focus();
    start();
}

/* ---------------- OPTION BUTTONS ---------------- */
function showOptions(options, callback) {
    input.disabled = true;
    const container = document.createElement("div");

    options.forEach(opt => {
        const btn = document.createElement("div");
        btn.className = "option-btn";
        btn.innerText = opt;

        btn.onclick = () => {
            user(opt);
            container.remove();
            input.disabled = false;
            input.focus();
            callback(opt);
        };

        container.appendChild(btn);
    });

    chat.appendChild(container);
    chat.scrollTop = chat.scrollHeight;
}

/* ---------------- ENTER KEY SUPPORT ---------------- */
input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});

/* ---------------- INIT ---------------- */
start();
