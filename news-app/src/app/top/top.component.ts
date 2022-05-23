import { Component, Input, OnInit } from '@angular/core';
import { AppModule } from '../app.module';

@Component({
  selector: 'app-top',
  templateUrl: './top.component.html',
  styleUrls: ['./top.component.css']
})
export class TopComponent implements OnInit {
  @Input() showLogin : Boolean = true;
  currentUser = AppModule.current_user;
  constructor() { }

  ngOnInit(): void {
  }

}
