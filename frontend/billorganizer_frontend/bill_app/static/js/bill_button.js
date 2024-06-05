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
async function add_all() {
    const response = await axios.get('/addall', { 
            params: { 
                rows: JSON.stringify(rows)
            } 
        });
        console.log(response.data);
  }


  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  async function handleNotes(num, bill_biennium, bill_bill_id) {
      const box = document.getElementById("notebox-" + num);

      if (box.hidden === true) {
          const note = await axios.get('/getnote/' + bill_biennium + '/' + bill_bill_id)
          console.log(note);
          document.getElementById(num + '-notelabel').value = note.data
          box.hidden = false
          document.getElementById(num + "-notebutton").textContent = "save"
      }
      else {
          document.getElementById(num + "-notebutton").textContent = "notes"
          const text = document.getElementById(num + '-notelabel').value
          console.log(text);
          await axios.put(`/writenote/${bill_biennium}/${bill_bill_id}/`, {
              text
          },
          {
              headers: {'X-CSRFToken': csrftoken}
          })
          box.hidden = true
          document.getElementById(num + "-notebutton").textContent = "note"
      }
  }
