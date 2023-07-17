const mainContent = document.getElementById("signup-main-content");
let isTermsArticleOpen = false;
const termsArticle = document.getElementById('termsOfUseArticle');


    // Hide the termsArticle by default when the page loads
termsArticle.style.display = 'none';



document.getElementById('termsOfUse').addEventListener('click', function(event){

    if (!isTermsArticleOpen) {
        termsArticle.style.display = 'block'; // Show the termsArticle by changing the display property
        isTermsArticleOpen=true;
        mainContent.classList.add('blurred');
    };       
});

document.getElementById('small-terms-times').addEventListener('click', function(event){

    if (isTermsArticleOpen) {
        termsArticle.style.display = 'none'; // Show the signup form again
        isTermsArticleOpen=false;
        mainContent.classList.remove('blurred');
    };       
});