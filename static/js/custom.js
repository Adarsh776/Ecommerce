  // Size/Storage selection
    document.querySelectorAll('.size-box').forEach(box => {
    box.addEventListener('click', function () {
      document.querySelectorAll('.size-box').forEach(el => el.classList.remove('selected'));
      this.classList.add('selected');
      const attr = this.closest('.product-options').querySelector('h3').innerText.split(" ")[1].toLowerCase();
      document.getElementById(`selected-${attr}`).value = this.dataset.size;
    });
  });

  // Quantity increment/decrement
  function updateQty(val) {
    const qtyInput = document.getElementById('qty');
    let current = parseInt(qtyInput.value);
    if (current + val >= 1) qtyInput.value = current + val;
  }


