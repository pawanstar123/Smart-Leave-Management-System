let leaveTypes = JSON.parse(localStorage.getItem("leaveTypes")) || [];

displayLeaveTypes();

let form = document.getElementById("leaveTypeForm");

if (form) {
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        let type = document.getElementById("leaveType").value;

        leaveTypes.push(type);

        localStorage.setItem("leaveTypes", JSON.stringify(leaveTypes));

        displayLeaveTypes();
        this.reset();
    });
}

function displayLeaveTypes() {
    let table = document.getElementById("leaveTypeTable");

    if (!table) return;

    table.innerHTML = `
        <tr>
            <th>Leave Type</th>
            <th>Action</th>
        </tr>
    `;

    leaveTypes.forEach((type, index) => {
        table.innerHTML += `
            <tr>
                <td>${type}</td>
                <td>
                    <button onclick="deleteType(${index})" class="delete">Delete</button>
                </td>
            </tr>
        `;
    });
}

function deleteType(index) {
    leaveTypes.splice(index, 1);

    localStorage.setItem("leaveTypes", JSON.stringify(leaveTypes));

    displayLeaveTypes();
}