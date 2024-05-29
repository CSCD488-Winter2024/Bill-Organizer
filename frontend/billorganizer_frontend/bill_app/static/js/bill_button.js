function setup(){ 
    var rows = JSON.parse("{{rows|escapejs}}"); 
    var rowheads = []
    for (var i = 0; i < rows.length; i++) {
      rowheads.push("rowhead"+i)
    } 
    for(var row in rowheads){ 
      
    } 
  }
  setup()
//   const bill_button = async (i) => {
//     //pass i to django for row index
//   const response = await axios.get('/request', { 
//       params: { 
//           row_index: i 
//       } 
//   });
//   console.log(response.data);
//   };
async function bill_button(i) {
    const response = await axios.get('/billbutton', { 
            params: { 
                row_index: i 
            } 
        });
        console.log(response.data);
  }