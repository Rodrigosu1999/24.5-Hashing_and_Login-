const URL = "http://localhost:5000/api";


/** given data about a cupcake, generate html */

function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}


/** put initial cupcakes on page. */

async function showInitialCupcakes() {
  const response = await axios.get(`${URL}/cupcakes`);

  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcakes-list").append(newCupcake);
  }
}

$("#cupcake-form").on("submit", async function(evt){
    evt.preventDefault();
    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const image = $("#image").val();
    
    const postResponse = await axios.post(`${URL}/cupcakes`,
    {
        flavor,
        size,
        rating,
        image
    });
    const newCupcake = generateCupcakeHTML(postResponse.data.cupcake);
    $("#cupcakes-list").append(newCupcake);
    $("#cupcake-form").trigger("reset");
});

$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
  
    await axios.delete(`${URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
  });

showInitialCupcakes();