// ==UserScript==
// @name         euracess_Save HTMLs
// @namespace    http://tampermonkey.net/
// @description  save htmls
// @version      2025-07-29
// @author       Parzi & ChatGPT
// @match        https://euraxess.ec.europa.eu/jobs/search?f%5B0%5D=keywords%3A*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==


(function () {
    'use strict';

    const keywordFromURL = (() => {
        const match = location.href.match(/keywords(?:%3A|:)([^&]+)/);
        return match ? decodeURIComponent(match[1]) : 'unknown';
    })();

    const safeKeyword = keywordFromURL.replace(/\s+/g, '_').replace(/[^\w\-]/g, '');

    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }


    function saveHTML(filename, content) {
        const blob = new Blob([content], { type: 'text/html' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    }

    async function saveAllPages() {
        let pageNum;

        while (true) {
            const pageParamMatch = location.href.match(/[?&]page=(\d+)/);
            if (pageParamMatch) {
                pageNum = parseInt(pageParamMatch[1]) + 1;
            } else {
                pageNum = 1;
            }
            console.log(`💾 Saving page ${pageNum} for "${safeKeyword}"`);

            await delay(2000); // buffer after load

            const htmlContent = document.documentElement.outerHTML;
            const filename = `euraxess_${safeKeyword}_page${pageNum}.html`;
            saveHTML(filename, htmlContent);


            // Find the "Next" button by text content
            const nextPageBtn = Array.from(document.querySelectorAll('a.ecl-pagination__link'))
            .find(a => a.textContent.trim().toLowerCase() === 'next');

            if (!nextPageBtn) {
                console.log('✅ No more pages.');

                break;
            }


            await delay(2000); // Optional: additional buffer

            // Click next
            nextPageBtn.click();


        }

        alert(`✅ Finished saving all pages for keyword "${safeKeyword}"`);
        window.location.href = `https://euraxess.ec.europa.eu/jobs/search`;
    }


    // Kick off
    saveAllPages();
})();

