import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Params} from "@angular/router";
import {MetadataService} from "./metadata.service";
import {Metadata} from "./metadata";

@Component({
  selector: 'app-metadata-detail',
  templateUrl: 'metadata-detail.component.html',
  styleUrls: ['metadata-detail.component.css']
})
export class MetadataDetailComponent implements OnInit {

  metadataItem: Metadata = null;

  constructor(
    private metadataService: MetadataService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.route.params.forEach((params: Params) => {
      let id = params['id'];
      this.metadataService.getMetadataDetail(id)
        .then(metadataItem => this.metadataItem = metadataItem);
    });
  }

}
