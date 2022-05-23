import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AppModule } from '../app.module';
import { User } from '../services/models';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {
  user = new User();
  currentuser = AppModule.current_user;
  message : String = '';

  constructor(private userService : UserService, private router : Router) { }

  ngOnInit(): void {
  }

  signUp(){
    console.log(this.user);
    this.userService.signUp(this.user).subscribe(res => {
      this.message = res.message;
      console.log(this.user);
      console.log(res.user);
      if(res.user != undefined){
        this.currentuser = res.user;
        this.router.navigate(['/main-site']);
      }
    })
  }
}
