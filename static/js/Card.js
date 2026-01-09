// Card.js
// to handle button clicks for incrementing and decrementing input value

  const input = document.getElementById("quantity-input");// get the input element
  const incrementBtn = document.getElementById("increment-button");// get the increment button
  const decrementBtn = document.getElementById("decrement-button"); // get the decrement button

  // add event listeners to buttons when user click take the info
  //+1
  incrementBtn.addEventListener("click", () => {
    input.value = Number(input.value) + 1;
  });
//-1
  decrementBtn.addEventListener("click", () => {
    if (Number(input.value) > Number(input.min)) {
      input.value = Number(input.value) - 1;
    }
  });
