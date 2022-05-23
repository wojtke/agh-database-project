import { Component, Input, OnInit } from '@angular/core';
import {Comment } from '../services/models'
import { CommentService } from '../services/comment.service';
import { AppModule } from '../app.module';

@Component({
  selector: 'app-add-comment-form',
  templateUrl: './add-comment-form.component.html',
  styleUrls: ['./add-comment-form.component.css']
})
export class AddCommentFormComponent implements OnInit {
  @Input() article_id : Number = 0;
  comment : Comment = new Comment;
  constructor(private commentService : CommentService) { }

  ngOnInit(): void {
  }
  publishComment(){
    this.comment.user_id = AppModule.current_user.user_id;
    this.comment.article_id = this.article_id;
    this.commentService.publishComment(this.comment);
  }
}
