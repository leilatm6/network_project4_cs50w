document.addEventListener('DOMContentLoaded',()=>{
    document.querySelector('#post').addEventListener('click',addpostfunc);
    const currentPage = document.getElementById('currentpage');
    console.log(currentPage.textContent)
    document.querySelectorAll('.paginationlink').forEach(link => {
        console.log('Found .paginationlink element:', link);
        link.addEventListener('click', () => {
            if (link.getAttribute('id') === 'firstpage') {
                updateContent(1);
            }
            if (link.getAttribute('id') === 'lastpage') {
                const lastpagenumber = link.getAttribute('data-page');
                console.log(lastpagenumber)
                updateContent(lastpagenumber); 
            }
            if (link.getAttribute('id') === 'nextpage') {
                const nextPageNumber = parseInt(currentPage.textContent) + 1;
                updateContent(nextPageNumber);
            }
            if (link.getAttribute('id') === 'previouspage') {
                const previousPageNumber = parseInt(currentPage.textContent) - 1;
                updateContent(previousPageNumber);
            }
        });
    
    });
    loadposts(1)
});



function addpostfunc(event){
    const posttext = document.querySelector('#posttext');
    fetch('/posts', {
        method: 'POST',
        body : JSON.stringify({
            posttext : posttext.value
        })
    }).then(response =>{
        console.log('Request sent');
        if (!response.ok){
            console.log('Response not ok');
            let error_message = 'Network response was not ok'; 
            return response.json().then(data =>{
                if (data.error){
                    error_message = data.error;
                }
                throw new Error(error_message);
            });
        }
        return response.json();
    }).then(result =>{
        console.log('Response received:', result);      
        loadposts(1);
    })
}


function loadposts(n){
    console.log('loadpost is loadeed',n)
    document.querySelector('#newpostcontainer').classList.add('hidden');
    document.querySelector("#postcontainer").innerHTML = '';   
    fetch(`/getposts/?page=${n}`)
        .then(response => response.json())
        .then(data => {        
            showpost(data)
        })
        .catch(error => {
            console.error('Error fetching posts:', error);
        });
   
}


function showpost(data){
    const posts = data.posts;
    const List = document.createElement('ul');
    List.setAttribute('class', "list-group");
    for (const post of posts) {
        const listItem = document.createElement('li');
        listItem.classList.add("list-group-item");      
                  
        listItem.innerHTML = post.text;
        List.appendChild(listItem);
    }
    document.querySelector('#postcontainer').appendChild(List);
    
    const firstLink = document.querySelector("#firstpage");
    const previousLink = document.querySelector("#previouspage");
    const pagenumber = document.querySelector('#currentpage');
    pagenumber.textContent = data.current_page;
    let nextLink = document.querySelector('#nextpage');
    let lastLink = document.querySelector("#lastpage");
    lastLink.setAttribute('data-page',value = data.total_pages);
                
    firstLink.classList.remove('disablelink')
    previousLink.classList.remove('disablelink')  
    nextLink.classList.remove('disablelink')
    lastLink.classList.remove('disablelink')
    if (data.current_page === 1) {
        console.log('disable')
        firstLink.classList.add('disablelink')
        previousLink.classList.add('disablelink')    
    }
    if (data.current_page === data.total_pages) {
        nextLink.classList.add('disablelink')
        lastLink.classList.add('disablelink')
    }
}


function updateContent(pageNumber) {
    loadposts(pageNumber);
}