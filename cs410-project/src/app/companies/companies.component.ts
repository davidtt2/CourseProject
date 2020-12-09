/* David Tan Sang Tran - UIUC - CS410 Fall 2020 */

import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import  *  as  data  from  './companies.json';

class company {
  companyName: string;
  logo: string;
  foundedDate: string; 
  founders: string;
  headquarters: string;
  companyLink: string;
  constructor (CompanyName: string, Logo: string, FoundedDate: string, 
               Founders: string, Headquarters: string, CompanyLink: string) {
    this.companyName = CompanyName;
    this.logo = Logo;
    this.foundedDate = FoundedDate;
    this.founders = Founders;
    this.headquarters = Headquarters;
    this.companyLink = CompanyLink;
  }
}

@Component({
  selector: 'app-companies',
  templateUrl: './companies.component.html',
  styleUrls: ['./companies.component.css']
})

export class CompaniesComponent implements OnInit {

  companiesList: Array<company> = [];
  dataSource = new MatTableDataSource<company>();
  searchText: string = "";
  displayNoRecords = false;

  constructor() { }

  ngOnInit(): void {
    console.log(data);
    for (let i = 0; i < data.length; i++) {
      this.companiesList.push(new company(
        data.data[i][0], data.data[i][1], data.data[i][2], 
        data.data[i][3], data.data[i][4], "https://" + data.data[i][5])
      );
    }

    this.dataSource.data = this.companiesList;
    this.dataSource.filterPredicate = function(data, filter: string): boolean {
      return data.companyName.toLowerCase().includes(filter);
    }
  }

  displayedColumns: string[] = ['logo', 'companyName', 'headquarters', 'foundedDate', 'founders'];

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
    
    if (this.dataSource.filteredData.length == 0) {
      this.displayNoRecords = true;
    } else{
      this.displayNoRecords = false;
    }
  }
}

/* David Tan Sang Tran - UIUC - CS410 Fall 2020 */