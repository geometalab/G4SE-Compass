import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-metadata-search',
  templateUrl: './metadata-search.component.html',
  styleUrls: ['./metadata-search.component.css']
})
export class MetadataSearchComponent implements OnInit {

  maxPerPage: number = 10;

  constructor() { }

  search(text, language){
    console.log("searchng: ", text, language, this.maxPerPage);
  }

  ngOnInit() {
  }

}
