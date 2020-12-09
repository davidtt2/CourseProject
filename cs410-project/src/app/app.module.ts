import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CompaniesComponent } from './companies/companies.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInput, MatInputModule } from '@angular/material/input';
import { MatSort, MatSortModule } from '@angular/material/sort';

@NgModule({
  declarations: [
    AppComponent,
    CompaniesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule, FormsModule,
    MatCardModule, MatTableModule, MatFormFieldModule, MatInputModule, MatSortModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
