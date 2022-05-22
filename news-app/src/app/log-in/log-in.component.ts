import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AppModule } from '../app.module'
import { User } from '../services/models';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {
  user = new User();
  users : User[] = [];
  userNotFound : Boolean = false;
  currentuser = AppModule.current_user;
  constructor(private userService : UserService, private router : Router) { }

  ngOnInit(): void {
    this.userService.getUsers().subscribe(data => this.users = data.users);
        console.log("success1");
  }

  logIn(){
    console.log(this.users);
    console.log(this.user);
    if(this.users == []){
          this.userService.getUsers().subscribe(data => this.users = data.users);
    }
    const newUser = this.users.find(user => {return this.user.login === user.login});
    if(newUser == undefined){
      this.userService.addUser(this.user).subscribe(user => AppModule.current_user = user);
    }
    else{
      AppModule.current_user = this.user;
      this.router.navigate(['main-site']);
    }
  }

}
