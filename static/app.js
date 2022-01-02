try{
    const searchbtn = document.querySelector("#btn");
    const searchText = document.forms[0].search;
    const load = document.querySelector("#loading");
    
    searchText.addEventListener("keydown", (e)=>{
        if(e.keyCode == 13){
            e.preventDefault();
            search(searchText.value);
        }
    }, true);
    
    searchbtn.addEventListener("click", ()=>{
        search(searchText.value);
    }, true);
    
    let container = [];
    async function search(wd="Ethiopia Orthodox mezmure"){
        container = [];
        load.className = "add";
        if(wd.length<=0) return;
        res = await fetch(window.location.href+"api/search="+wd)
        .then(data => data.json())
        .then((val)=>{update(val)});
    }
    
    function update(val){
        val.inf.forEach(index=>{
            index = Object.values(index)[0];
            container.push(index);
        });
        update_display();
    }
    
    search();
    const cont = document.querySelector(".container");
    

    
    function update_display(){
        if(container.length == 0){
            load.className = "remove";
            cont.innerHTML = `<b><h1>No result found for "${searchText.value}"</h1> </b>`;
            return false;
        }
            cont.innerHTML = "";
        setTimeout(()=>{
            container.forEach((index)=>{
                if(index[0].length!=0){
                    load.className = "remove";
                    poster = `https://i.ytimg.com/vi/${index[1]}/hqdefault.jpg`;
                    cont.innerHTML += `
                      <div class='each'> 
                        <video  src= "${index[0]}" controls autostart="false" preload="none" poster="${poster}" class="item"  width="560" height="315" ></video>
                        <!--<b>${index[0]}</b> -->
                        </div>
                        `;
                }
                });
        }, 1);
    }
    }catch(e){
        alert("Error just happened! contact the administer.\n Error:"+e);
    }
    