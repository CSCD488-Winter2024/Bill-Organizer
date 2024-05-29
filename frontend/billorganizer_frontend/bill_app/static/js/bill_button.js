var rows = []
function setup(){ 
    rows = JSON.parse("{{js_rows|escapejs}}"); //todo why does this break???
    console.log(rows)
  }
setup()
async function bill_button(i) {
    const response = await axios.get('/billbutton', { 
            params: { 
                row: JSON.stringify(rows[i])
            } 
        });
        console.log(response.data);
  }