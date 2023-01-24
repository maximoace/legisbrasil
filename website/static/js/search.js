const dataRowTemplate = document.querySelector("[data-row-template]")
const dataContainer = document.querySelector("[data-container]")
const searchInput = document.querySelector("[data-search]")

let deputies = []

searchInput.addEventListener("input", (e) =>{
    const value = e.target.value.toLowerCase()
    deputies.forEach(deputy => {
        const isVisible = deputy.name.toLowerCase().includes(value)
        deputy.element.classList.toggle("hide", !isVisible)
    })
})

fetch('/fetchTable')
.then(res => res.json())
.then(data => {
    deputies = data.map(deputy =>{
        const row = dataRowTemplate.content.cloneNode(true).children[0]
        const name = row.querySelector("[data-name]")
        const party = row.querySelector("[data-party]")
        const state = row.querySelector("[data-state]")
        const status = row.querySelector("[data-status]")
        const link = row.querySelector("[data-link]")
        name.textContent = deputy.name
        party.textContent = deputy.party
        state.textContent = deputy.state
        status.textContent = deputy.status
        link.href = `/details/${deputy.id}`
        dataContainer.append(row)
        return {name: deputy.name, element: row}
    })
})