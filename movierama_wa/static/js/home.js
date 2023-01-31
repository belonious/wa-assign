let ORDERING = ''
const getCSRFT = () => {
    return document.querySelector("[name='csrfmiddlewaretoken']").value
}
const getData = async () => {
    const r = await fetch(`/api/movies/${ORDERING ? '?ordering='+ORDERING : ''}`)
    const data = await r.json()
    return data;
}
const opinionDeletion = async (movie) => {
    const payload = {
        movie_id: movie
    }

    const res = await fetch('/users/submit_opinion/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFT()
        },
        body: JSON.stringify(payload)
    })

    if (res.ok) {
        renderMovieList()
    }else {
        const resJson = await res.json()
        alert(resJson)
    }
}
const opinionSubmit = async (movie, liked) => {
    const payload = {
        movie_id: movie,
        liked
    }

    const res = await fetch('/users/submit_opinion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFT()
        },
        body: JSON.stringify(payload)
    })

    if (res.ok) {
        renderMovieList()
    }else {
        const resJson = await res.json()
        alert(resJson)
    }
}
const getDateDisplay = (dateCeated) => {
    const dif = Math.abs(Date.now() - new Date(dateCeated)) / 36e5;
    if (dif >=24) {
        return `${Math.round(dif / 24)} days`;
    }
    return `${Math.round(dif)} hours`;
}
const getOpinionTpl = (movie) => {
    // console.log(movie.aggr_opinions.liked);
    const actionsClass = {
        like: `m${movie.id} like-submit`,
        hate: `m${movie.id} hate-submit`,
        remove: `m${movie.id} remove-opinion`,
    }
    if (!movie.aggr_opinions.liked){
        return `<div>\
        <button class="btn ${actionsClass.like} btn-success" data-movie="${movie.id}">Like</button>\
        <button class="btn ${actionsClass.hate} btn-danger" data-movie="${movie.id}">Hate</button>\
</div>`
    }
    return `<div>\
        <button class="btn ${actionsClass.remove} btn-info" data-movie="${movie.id}">\
        Remove ${movie.aggr_opinions.liked.value ? 'like' : 'hate'}</button>\
</div>`
}
const getMovieTpl = movie => {
    const postAge = getDateDisplay(movie.date_created);
    const opinionTpl = USER_LOGGED_IN ? getOpinionTpl(movie) : ''
    return `<div>\
    <h3>${movie.title}</h3>\
    <div class="user-${movie.submitted_by.id}">Posted by ${movie.submitted_by.username}\
    ${postAge} ago</div>\
    <div>${movie.description}</div>\
    <div>likes ${movie.aggr_opinions.opinions.likes} |\
    hates ${movie.aggr_opinions.opinions.hates}</div>\
    ${opinionTpl}\
    </div>`
}
const addEventBindings = () => {
    const likeSubmitEls = [ ...document.getElementsByClassName("like-submit")]
    likeSubmitEls.forEach(el => {
        el.addEventListener('click', e => opinionSubmit(e.target.dataset.movie, true) )
    })
    const hateSubmitEls = [ ...document.getElementsByClassName("hate-submit")]
    hateSubmitEls.forEach(el => {
        el.addEventListener('click', e => opinionSubmit(e.target.dataset.movie, false) )
    })
    const removeOpinionEls = [ ...document.getElementsByClassName("remove-opinion")]
    removeOpinionEls.forEach(el => {
        el.addEventListener('click', e => opinionDeletion(e.target.dataset.movie) )
    })
}

const setMovieContainerTpl = movies => {
    const moviesContainer = document.getElementById('moviesContainer')
    const moviesContainerTpl = movies.reduce((finalTpl, movie) => {
        const movieTpl = getMovieTpl(movie);
        finalTpl += movieTpl;
        return finalTpl;
    }, '')
    moviesContainer.innerHTML = moviesContainerTpl;
}
const renderMovieList = async (ordering) => {
    if (ordering){
        ORDERING = ordering;
    }
    const movies = await getData()
    setMovieContainerTpl(movies)
    addEventBindings()
}
const init = async () => {
    console.log('INIT')
    const orderByEls = [ ...document.getElementsByClassName("order_by")]
    orderByEls.forEach(el => {
        el.addEventListener('click', e => renderMovieList(e.target.dataset.order) )
    })
    renderMovieList()
}

window.onload = function() {
    init();
};
