const fillDataList = async function () {
    const response = await fetch("/static/people.json");
    const people = await response.json();
    const datalist = document.getElementById("autocomplete");
    people.forEach(element => {
        let newOption = document.createElement("option");
        newOption.setAttribute("value", element.id);
        datalist.appendChild(newOption);
    });
};

fillDataList();