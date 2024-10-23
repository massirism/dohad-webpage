document.addEventListener('DOMContentLoaded', () => {
    const addKeywordButton = document.getElementById('addKeyword');
    const keywordInput = document.getElementById('keywords');
    const keywordList = document.getElementById('keywordList');
    const recommendForm = document.getElementById('recommendForm');
  
    addKeywordButton.addEventListener('click', () => {
        const keyword = keywordInput.value.trim();
        if (keyword) {
            const listItem = document.createElement('li');
            listItem.textContent = keyword;
            keywordList.appendChild(listItem);
            keywordInput.value = '';
            keywordInput.focus();
        }
    });
  
    recommendForm.addEventListener('submit', (event) => {
        const keywords = [];
        keywordList.querySelectorAll('li').forEach(item => {
            keywords.push(item.textContent);
        });
        if (keywords.length > 0) {
            keywordInput.value = keywords.join(',');
        } else {
            event.preventDefault();
            alert('Please add at least one keyword.');
        }
  
    });
  });
  