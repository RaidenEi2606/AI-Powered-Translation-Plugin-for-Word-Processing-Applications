const fetch = require("node-fetch"); // Cần cài đặt thư viện này

async function testFetch() {
    try {
        const response = await fetch("http://127.0.0.1:3000/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: "Hello", source_lang: "English", target_lang: "Vietnamese" })
        });

        const data = await response.json();
        console.log("✅ Kết quả:", data);
    } catch (error) {
        console.error("❌ Lỗi:", error);
    }
}

testFetch();
