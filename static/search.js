
function highlightSearch() {
var searchQuery = document.getElementById('search').value.toLowerCase();
var table = document.getElementById('data-table');
var rows = table.getElementsByTagName('tr');

for (var i = 1; i < rows.length; i++) {
var cells = rows[i].getElementsByTagName('td');
var rowMatch = false;

for (var j = 0; j < cells.length; j++) {
    var cell = cells[j];
    var cellText = cell.textContent.toLowerCase();

    if (cellText.includes(searchQuery)) {
        rowMatch = true;
        cell.innerHTML = cell.innerHTML.replace(new RegExp(searchQuery, 'gi'), '<span class="highlight">$&</span>');
    } else {
        cell.innerHTML = cellText;
    }
}

if (rowMatch) {
    rows[i].style.display = '';
} else {
    rows[i].style.display = 'none';
}
}
}
