import { Injectable, signal, WritableSignal } from "@angular/core";

@Injectable({
    providedIn: 'root'
})

export class ChatService {
    isChatWindowOpen: WritableSignal<boolean> = signal(false);

    toggleChatWindow() {
        this.isChatWindowOpen.update((currentValue) => !currentValue);
    }
}