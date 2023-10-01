import { useCallback, useEffect, useRef, useState } from "react";
import { v4 as uuidv4 } from 'uuid';

function AddObit({ closePop }){
    const [name, setName] = useState("");
    const [born, setBorn] = useState("");
    const [died, setDied] = useState("");
    const [file, setFile] = useState(null);
    const [isFilled, setIsFilled] = useState(true);
    
    const close = () => {
        closePop();
    };

    const submitObit = async () => {

        document.getElementById("submit-btn").disabled = true;
        const data = new FormData();
        data.append("file",file);

        if(file === null || name === "" || born === "" || died === ""){
            setIsFilled(false);
        } else{
            setIsFilled(true);
            document.getElementById("submit-btn").innerHTML = "Generating... Please wait";
            const url = "https://lnbecc25kn3p47pvfz473zofru0zpkuk.lambda-url.ca-central-1.on.aws/"+
            
            `?name=${name}&year_born=${born}&year_died=${died}`;
            const res = await fetch(url, {
                method: "POST",
                headers:{
                    "Authentification": "",
                    "id": uuidv4()
                  },
                body: data,
                }
            );
            try{
                const response_content = await res.json();
                const values = JSON.parse(response_content);
            }   catch{
                //console.log("error");
            }
            
            close();
            document.getElementById("submit-btn").disabled = false;
        }
    };



    const onFileChange = (e) =>{
        setFile(e.target.files[0]);
        document.getElementById("filename").innerHTML = "(" + e.target.files[0].name + ")";
    };

    const onBornChange = (e) => {
        setBorn(e.target.value);
    };

    const onDiedChange = (e) => {
        setDied(e.target.value);
    };
    

    return(
        <div id="pop-container">
            <button onClick={close} id="esc-btn">X</button>
            <h1>Create a New Obituary</h1>
            <img id="flower-img" src="https://i.ibb.co/RbvsPfY/Pngtree-european-flower-love-diamond-glide-7465107.png" border="0" alt="My Image" width="0" height="200"></img>
            <form>
                <label>
                    Select an image for the deceased 
                    <input id="file-in" type="file" required accept="images/*" onChange={(e) => onFileChange(e)}/>
                    <span id="filename"></span>
                </label>
                <br/>
                <input id="name-in" type="text" placeholder="Name of the deceased" value={name} onChange={(e) => setName(e.target.value)}/>
                <div id="dates-in">
                    <p>Born:  <input onChange={onBornChange} type="date"/></p>
                    <p>Died:  <input onChange={onDiedChange} type="date"/></p>
                </div>
                {isFilled ? (<></>) : (<p id="error-msg">Please make sure that all fields are filled</p>)}
                <button id="submit-btn" type="button" onClick={submitObit}>Write Obituary</button>
            </form>
        </div>
    );
}

export default AddObit;