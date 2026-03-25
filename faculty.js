let facultyList = JSON.parse(localStorage.getItem("facultyList")) || [];

// Display on load
if (document.getElementById("facultyTable")) {
    displayFaculty();
}

// Form submit
let form = document.getElementById("facultyForm");

if (form) {
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        let name = document.getElementById("name").value;
        let email = document.getElementById("email").value;
        let department = document.getElementById("department").value;

        // ✅ Added status
        let faculty = { name, email, department, status: "Active" };

        facultyList.push(faculty);

        localStorage.setItem("facultyList", JSON.stringify(facultyList));

        displayFaculty();
        this.reset();
    });
}

function displayFaculty() {
    let table = document.getElementById("facultyTable");

    if (!table) return;

    table.innerHTML = `
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th>Status</th>
            <th>Action</th>
        </tr>
    `;

    facultyList.forEach((f, index) => {
        table.innerHTML += `
            <tr>
                <td>${f.name}</td>
                <td>${f.email}</td>
                <td>${f.department}</td>
                <td>${f.status || "Active"}</td>
                <td>
                    <button onclick="toggleStatus(${index})">
                        ${f.status === "Inactive" ? "Activate" : "Deactivate"}
                    </button>
                    <button onclick="deleteFaculty(${index})" style="background:red;color:white;">
                        Delete
                    </button>
                </td>
            </tr>
        `;
    });
}

function deleteFaculty(index) {
    facultyList.splice(index, 1);

    localStorage.setItem("facultyList", JSON.stringify(facultyList));

    displayFaculty();
}

// ✅ NEW FUNCTION (SRS IMPORTANT)
function toggleStatus(index) {
    if (!facultyList[index].status) {
        facultyList[index].status = "Active";
    }

    facultyList[index].status =
        facultyList[index].status === "Active" ? "Inactive" : "Active";

    localStorage.setItem("facultyList", JSON.stringify(facultyList));

    displayFaculty();
}