// import logo from './logo.svg';
import './style.css'; 
import {useState, useEffect, useRef} from 'react';

function App() {
  const state_default = {
    user : {"id": null, "username": null, "authenticated": null, "comments": []},
    noSearch : null,
    noRating : null,
    madeComment : null,
    movieID : null,
    title : null,
    tagline : null,
    genres: null,
    poster_path : null,
    wiki_url : null,
    movieComments : []
  }
  const [data, setData] = useState(state_default);
  const [movieCommentsList, setMovieCommentsList] = useState(null);
  const [userCommentDiv, setUserCommentDiv] = useState(null);
  const userComment = useRef(null)
  const deletedUserComment = useRef(false);
  const editedUserComment = useRef(false);

  function getUserComment(comments, userID){
    for (let i in comments){
      if (comments[i]["userID"] === userID){
        return comments.splice(i, 1)[0];
      }
    }
    return null;
  }

  /* function is called when the template is finished rendering */
  useEffect(() => {
    const args = (document.getElementById("data") == null) ? (state_default) : JSON.parse(document.getElementById("data").text);
    const us = getUserComment(args["movieComments"], args["user"]["id"]);
    setData(args);
    userComment.current = us;

    setMovieCommentsList(args["movieComments"].map(movieCommentsHTML));
    setUserCommentDiv(userCommentHTML());
  }, []);

  console.log(data);
  console.log(userComment);
  console.log(deletedUserComment);

  const rateTitle = {
    marginTop: "30px",
    marginBottom: "30px",
    fontFamily: "sans-serif",
    fontWeight: "500"
  };

  const madeComment = {
    marginTop: "5px",
    marginBottom: "15px"
  };

  const commentBox = {
    marginTop: "20px",
    fontSize: "18px"
  };

  function saveComment(){   
    /* event.preventDefault(); */ 
    let comment = userComment.current;
    let formData = new FormData();
    formData.append("comment_json", JSON.stringify(comment));
    formData.append("to_delete", deletedUserComment.current);
    formData.append("edited", editedUserComment.current);

    fetch("/comment", {method: "POST", body: formData})
    .then((response) => response.json())
    .then((dt) => {
      if (dt["success"] === true){
        console.log(dt["success"]);
        commitDelete();
      } else {

      }
    });
  }
  function commitDelete(){
    setUserCommentDiv(() => {
      return (
        <div class="deleted-message">
          <p class="line">Your changes have been saved.</p>
        </div>
      )
    });
  }
  function handleEdit(){

  }

  function undoDelete(){
    deletedUserComment.current = false;
    setUserCommentDiv(userCommentHTML());
  }

  function handleDelete(){
    function set(comment) {
      if (comment == null) {
        return (<div></div>);
      }
      else {
        return (
          <div class="comment deleted-comment">
            <p class="line deleted-comment" style={{marginBottom: "16px"}}><span id="username1" style={{color: "rgb(211, 238, 255)"}}>{comment.username}</span> - {comment.rating}
              {(() => {
                if (comment.rating === 1){
                  return (<span> star</span>)
                } else {
                  return (<span> stars</span>)
                }
              })()}
              <span style={{float: "right"}} class="">
                <button id="edit-comment" type="button" class="button" style={{marginRight: "4px", borderColor: "purple", backgroundColor: "purple"}} onClick={() => saveComment()}>Save</button>
                <button id="delete-comment" type="button" class="button" style={{marginLeft: "4px"}} onClick={() => undoDelete()}>Undo</button>
              </span>
            </p>
            <p class="line deleted-comment">{comment.comment}</p>
          </div>
        )
      }
    }
    deletedUserComment.current = true;
    setUserCommentDiv(set(userComment.current));
  }

  /* create a div for the current user's comment, has options to edit or delete */
  function userCommentHTML(){
    let comment = userComment.current;
    if (comment == null) {
      return (<div></div>);
    }
    else {
      return (
        <div class="comment">
          <p class="line" style={{marginBottom: "16px"}}><span id="username1">{comment.username}</span> - {comment.rating}
            {(() => {
              if (comment.rating === 1){
                return (<span> star</span>)
              } else {
                return (<span> stars</span>)
              }
            })()}
            <span style={{float: "right"}} class="">
              <button id="edit-comment" type="button" class="button" style={{marginRight: "4px"}} onClick={() => handleEdit()}>Edit</button>
              <button id="delete-comment" type="button" class="button" style={{marginLeft: "4px"}} onClick={() => handleDelete()}>Delete</button>
            </span>
          </p>
          <p class="line">{comment.comment}</p>
        </div>
      )
    }
  };
  /* map other users' comments */
  function movieCommentsHTML(comment){
    return (
      <div class="comment">
        <p class="line"><span id="username1">{comment.username}</span> - {comment.rating}
          {(() => {
            if (comment.rating === 1){
              return (<span> star</span>)
            } else {
              return (<span> stars</span>)
            }
          })()}
        </p>
        <span></span>
        <p class="line">{comment.comment}</p>
      </div>
    )
  };

  return (
    <div>
      <h1 id="welcome">Hello, <span id="username">{data["user"]["username"]}</span></h1>
      <form method="POST" action="/logout">
          <input type="submit" id="logout" value="Logout" class="button"/>
      </form>
      <form method="POST" action="/react" class="center">
          <input type="text" name="query" id="query" placeholder="Movie Name"/><br/>
          <input type="submit" value="Search TMDB" class="button"/>
      </form>
      {(() => {
        if (data["noSearch"] === true){
          return (<p id="result" class="center alert">No results. Random movie generated</p>)
        }
      })()}
      <h1 id="title" class="center">{data["title"]}</h1>
      <h1 id="genres" class="center">{data["genres"]}</h1>
      <h1 id="tagline" class="center">{data["tagline"]}</h1>
      {(() =>{
        if (data["wiki_url"] != null){
          return (<a id="wiki" href={data["wiki_url"]} class="center">Wikipedia</a>)
        }
      })()}
      <img id="poster" class="center" src={data["poster_path"]} alt="Movie Poster"></img>
      <h1 id="rate-movie" class="center" style={rateTitle}>Rate {data["title"]}</h1>
      {(() => {
        if (data["noRating"] === true){
          return (<p id="rating" class="center alert" style={madeComment}>Please rate the movie before submitting.</p>)
        }
      })()}
      {(() => {
        if (data["madeComment"] === true){
          return (<p id="made-comment" class="center alert" style={madeComment}>You already rated this movie.</p>)
        }
      })()}
      <form method="POST" action="/react" id="ratingForm" class="center">
          <input type="radio" id="1star" name="rating" value="1"/>
          <label for="1star">1 star</label>
          <input type="radio" id="2star" name="rating" value="2"/>
          <label for="2star">2 stars</label>
          <input type="radio" id="3star" name="rating" value="3"/>
          <label for="3star">3 stars</label>
          <input type="radio" id="4star" name="rating" value="4"/>
          <label for="4star">4 stars</label>
          <input type="radio" id="5star" name="rating" value="5"/>
          <label for="5star">5 stars</label>
          <textarea class="center" style={commentBox} id="comment-box" name="comment" rows="5" cols="40" placeholder="Enter your comment here"></textarea>
          <br/>
          <input type="hidden" name="movieID" value={data["movieID"]}/>
          <input type="submit" name="comment+rating" value="Submit" class="button"/>
      </form>
      {userCommentDiv}
      {movieCommentsList}
      <br/>
    </div>
  );
}

export default App;
