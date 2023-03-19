import { Component, OnInit, Input, ChangeDetectorRef  } from '@angular/core';
import { IngredientServiceService } from '../ingredient-service.service';
import { NgbModal, NgbActiveModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { Ingredient, NewIngredient } from '../../shared/models';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  @Input()
  searchQuery: string = '';

  selectedNewIngredient: number | null = null;

  searchResults: Ingredient[] = [];

  newIngredientModalRef: any;

  currentNewIngredients: NewIngredient[] = [];

  constructor(private ingredientService: IngredientServiceService, private modalService: NgbModal, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.ingredientService.getNewIngredients().subscribe(result => {
      this.currentNewIngredients = result.results;
    });
  }

  openNewIngredientModal() {
    // Get the modal template
    const modalRef = this.modalService.open(NgbdModalContent);
    // Set the modal's input data
    modalRef.componentInstance.modalTitle = 'Create New Ingredient';
    // Handle the modal's response when it closes
    modalRef.result.then((result) => {
      if (result) {
        this.currentNewIngredients.push(result);
      }
    }).catch((error) => {
      console.log(error);
    });
    // Set the modal reference for later use
    this.newIngredientModalRef = modalRef;
  }

  searchRelatedIngredients(): void {
    if (!this.selectedNewIngredient) {
      return;
    }
    this.ingredientService.searchRelatedIngredients(this.selectedNewIngredient).subscribe(result => {
      console.log(result)
      this.searchResults = result.results;
      console.log(this.searchResults);
    });
  }

  onNewIngredientSelected(event: any, ingredient: Ingredient) {
    // find the newIngredient object
    const newIngredient = this.currentNewIngredients.find(
      (ni) => ni.name === event.target.value
    );
    if (newIngredient) {
      this.createIngredientSynonym(ingredient, newIngredient);
      ingredient.newIngredient = newIngredient;
    }
    // detect changes to update the view
    this.cdr.detectChanges();
  }

  createIngredientSynonym(selectedNewIngredient: NewIngredient, ingredient: Ingredient): void {
    this.ingredientService.createIngredientSynonym(selectedNewIngredient.id, ingredient.id).subscribe(() => {
      // update the ingredient object with the selected new ingredient
      ingredient.newIngredient = selectedNewIngredient;
    });
  }


  searchIngredients(){
    if (!this.searchQuery) {
      return;
    }
    this.ingredientService.searchIngredients(this.searchQuery).subscribe(result => {
      this.searchResults = result.results;
    });
  }
}

// Define a new component for the modal's content
@Component({
  selector: 'ngbd-modal-content',
  template: `
    <div class="modal-header">
      <h4 class="modal-title">{{ modalTitle }}</h4>
      <button type="button" class="close" aria-label="Close" (click)="closeModal()">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="modal-body">
      <input type="text" class="form-control" [(ngModel)]="newIngredientName" placeholder="New Ingredient Name">
    </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-secondary" (click)="closeModal()">Cancel</button>
      <button type="button" class="btn btn-primary" (click)="createNewIngredient(newIngredientName)">Create</button>
    </div>
  `
})
export class NgbdModalContent {
  modalTitle: string = '';
  @Input()
  newIngredientName: any = '';

  constructor(private ingredientService: IngredientServiceService, public activeModal: NgbActiveModal) {}

  closeModal() {
    this.activeModal.close();
  }

  createNewIngredient(name: string) {
    this.ingredientService.createNewIngredient(name).subscribe(result => {
      this.activeModal.close(result);
    })
  }
}




