/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */



/* global document, Office, Word */

Office.onReady((info) => {
    if (info.host === Office.HostType.Word) {
        document.getElementById("sideload-msg").style.display = "none";
        document.getElementById("app-body").style.display = "flex";
        
        document.getElementById("translated-text");
        document.getElementById("translate-btn").onclick = run;
    }
  });

  const fetch = require("node-fetch");
  let lastTranslatedText = "";

  async function translateText(text, sourceLang, targetLang) {
    const url = "http://127.0.0.1:3000/translate";  // Địa chỉ API

    const data = {
        text: text,
        source_lang: sourceLang,
        target_lang: targetLang
    };

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            console.log("🔄 Bản dịch:", result.translated_text);
            lastTranslatedText = result.translated_text;  // Lưu kết quả vào biến toàn cục
            return lastTranslatedText;
        } else {
            lastTranslatedText = "❌ Lỗi:" + result.error ;
            return lastTranslatedText;
        }
    } catch (error) {
        lastTranslatedText = "❌ Lỗi kết nối API:" + error;
        return lastTranslatedText;
    }
}

  async function run() {
    try {
        await Word.run(async (context) => {
            const selection = context.document.getSelection();
            selection.load("text"); // Nạp nội dung được chọn

            await context.sync();

            const inputTextField = document.getElementById("input-text");
            const selectedText = selection.text.trim();

            // Nếu có đoạn được chọn -> đổ vào ô input
            if (selectedText.length > 0) {
                inputTextField.value = selectedText;
            }
            const sourceLang = document.getElementById("source-lang").value;
            const targetLang = document.getElementById("target-lang").value;
            const translatedTextField = document.getElementById("translated-text");

            let translated = await translateText(inputTextField.value, sourceLang, targetLang);
            console.log("✅ Kết quả nhận được:", translated);

            // Kiểm tra nếu có kết quả dịch, thì chèn vào Word
            if (translated) {
                translatedTextField.value = translated;
                
            }
        });
    } catch (error) {
        console.error("Lỗi: ", error);
    }                  
  }
