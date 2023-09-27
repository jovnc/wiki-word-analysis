svg = document.getElementById("results");
table_result = document.getElementById("results_table")

window.addEventListener("DOMContentLoaded", () => {
    svg.style.display = "block";
    table_result.style.display = "none";
})

wordcloud = document.querySelector("#wordcloud");
table = document.querySelector("#table");

wordcloud.addEventListener("click", () => {
    svg.style.display = "block";
    table_result.style.display = "none";
})

table.addEventListener("click", () => {
    svg.style.display = "none";
    table_result.style.display = "block";
})