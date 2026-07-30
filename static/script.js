//store all emotion cards from the html page in a variable so that we can add click functionality,all five div classed emotioncards are collected
const emotionCards =document.querySelectorAll(".emotion-card");
//visit every emotion card one by one,
//forEach()  viists each emotion card one by one
//'card' is a temporary variable representing current emotion and (card) means the new version of js meaninig funtion(card)
//=> is an arrow funtion tells js what to do for each card
const selectedEmotion = document.querySelector("#selectedEmotion");
//we created selectedEmotion because it will represent the hidden input that stores selected emotion
emotionCards.forEach((card) => {
    //when the current emotion card is clicked
    //addEventListener() attached to listen curent emotion
    //() => only run inside { } after user clicks
    //SYNTAX is object.addEventListener(event, function_to_run)
    card.addEventListener("click", () => {
        //remove the selected style from all emotion cards
        emotionCards.forEach((card)=>{
            //classList = stores all css classes attached to an html element
            //add = adds a new css class to the html element
            //remove() = removes a css class from the html element
            //take this card ->open its class list ->add the "selected" class
            card.classList.remove("selected");
        });
        card.classList.add("selected");
        //css notices the "selected" class and applies the css style to the selected card
        //classList contains emotionCard and selected classes, so the selected card has both styles applied to it
        selectedEmotion.value = card.querySelector(".emotion-name").textContent;
        //card is the emotion card and .textcontent reads the name of the emotion and selectedEmotion.value = stores "Happy" inside the hidden input
     });
}); //the above code is making the emotion cards selective and interactive

 const thoughtBox = document.querySelector(".thought-box");
 const counter = document.querySelector(".counter");
 //input event runs evrytime the user types in the thought box, so we can update the counter
 if(thoughtBox){
    thoughtBox.addEventListener("input", () => {
    const count=thoughtBox.value.length;
    //count the total number of the characters typed
    counter.textContent = `${count}/10,000`;
    //display the updated character count on the page
 });
}


 //this is the workflow of side bar 
const menuButton = document.querySelector(".menu-btn");
//find the first element whose clas is menu-btn and stores in te created variable menubutton
const sideBar = document.querySelector(".sidebar");

menuButton.addEventListener ("click",function(){
    console.log("Menu button clicked");
    //when someone clicks you execute this function
    if(sideBar.style.left == "0px"){
         //inside quotes because its a css value
    //js is talking to html using variables
    sideBar.style.left = "-250px";
    }
    else{
        sideBar.style.left = "0px";
    }
});



