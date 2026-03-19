function showSection(sectionId) {
    // Hide all sections
    let sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    // Show selected section
    document.getElementById(sectionId).style.display = 'block';
}