// ==UserScript==
// @name         findaphd_Search Keywords
// @namespace    http://tampermonkey.net/
// @version      2025-07-29
// @description  Search keywords on Euraxess job offers and save all result pages' HTML files
// @author       Parzi & ChatGPT
// @match        https://www.findaphd.com/phds/
// @grant        none
// ==/UserScript==



(function() {
    'use strict';

    // Helper: Delay for X ms
    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // run only when new round of keywords
    if (localStorage.getItem('keywords') === null){
        // Get the keyword input from user (comma separated)
        let input = prompt("Enter your keywords separated by commas:");
        if (!input) return;
        const keywords = input.split(',').map(k => k.trim()).filter(k => k.length > 0);
        if (keywords.length === 0) {
            alert("No valid keywords entered.");
            return;
        }

        localStorage.setItem('keywords', JSON.stringify(keywords));
        localStorage.setItem('index', 0);
    }

    // get the keyword
    let keywords = JSON.parse(localStorage.getItem('keywords') || '[]');
    let index = parseInt(localStorage.getItem('index') || '0', 10);

    // stop the script when all keywords are researched
    if (index >= keywords.length) {
        localStorage.removeItem('keywords')
        localStorage.removeItem('index')
        console.log("✅ Done: All keywords processed and cleaned the localStorage.");
        return; // Stops the script from continuing
    }

    let keyword = keywords[index];
    index++;
    localStorage.setItem('index', index);


    delay(2000)
    window.location.href = `https://www.findaphd.com/phds/?Keywords=${keyword}`;

})();
