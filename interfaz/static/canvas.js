
const container = document.querySelector("#container");
const newGridButton = document.querySelector("#new-grid")

function displayGrid(dimentions){
    for (let i = 0; i < dimentions; i++){
        const gridRow = document.createElement('div');
        gridRow.setAttribute("id", i);
        gridRow.classList.add('row')
        container.appendChild(gridRow);

        for (let j = 0; j < dimentions; j++){
            const gridCol = document.createElement('div');
            gridCol.setAttribute("id", i + "_" + j);
            gridCol.classList.add('col')
            gridRow.appendChild(gridCol);
        }
    }


    document.querySelectorAll(".col").forEach((cell) => {
        cell.addEventListener('mouseover', () => {
            cell.classList.add('colored');
        })
    })
}
