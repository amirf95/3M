
  const input = document.getElementById("quantity-input");
  const incrementBtn = document.getElementById("increment-button");
  const decrementBtn = document.getElementById("decrement-button");

  incrementBtn.addEventListener("click", () => {
    input.value = Number(input.value) + 1;
  });

  decrementBtn.addEventListener("click", () => {
    if (Number(input.value) > Number(input.min)) {
      input.value = Number(input.value) - 1;
    }
  });
