import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Comment } from './models'

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private commentsUrl = 'http://localhost:5001/comments';
  private  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    })
  };

  constructor(private http : HttpClient) { }

  getCommentsForArticle(id : Number) : Observable<Comment[]>{
    return this.http.get<Comment[]>(this.commentsUrl + '/article/' + id.toString());
  }

  publishComment(comment : Comment){
    this.http.post<Comment>(this.commentsUrl, comment, this.httpOptions);
  }
}
