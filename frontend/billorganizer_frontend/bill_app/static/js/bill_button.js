function setup(){ 
    // rows = JSON.parse(); //todo why does this break???
    // rows = "{{rows|safe}}";
    console.log(rows[0]);
  }
setup();
async function bill_button(i) {
    const response = await axios.get('/billbutton', { 
            params: { 
                row: JSON.stringify(rows[i])
            } 
        });
        console.log(response.data);
  }