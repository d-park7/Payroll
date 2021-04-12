const button = document.getElementById('clockIn');

button.addEventListener('click', async _ => {
  try {     
    const response = await fetch('user.html', {
      method: 'post',
      body: {
        // Your body
      }
    });
    console.log('Completed!', response);
  } catch(err) {
    console.error(`Error: ${err}`);
  }
});