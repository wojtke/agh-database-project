import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { switchMap } from 'rxjs';
import { ArticleService } from '../services/article.service';
import { CommentService } from '../services/comment.service';
import { Article, Comment } from '../services/models';

@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css']
})
export class ArticleComponent implements OnInit {
  article : Article = new Article;
  comments : Comment[] = [];
  commentsAvailable = false;

  constructor(private route : ActivatedRoute,  private articleService : ArticleService, private commentService : CommentService) { }

  ngOnInit(): void {
    let obs = this.route.paramMap.pipe(
      switchMap(params =>{
        let id = Number(params.get('id'));
        return this.articleService.getArticleById(id);
      })
    )
    obs.subscribe(data => {
      this.article = data;
    })

    this.commentService.getCommentsForArticle(this.article.article_id).subscribe(data =>{
      this.comments = data;
      if(this.comments.length > 0){
        this.commentsAvailable = true;
      }
    })
  }



}
