import { Component, Input } from "@angular/core";

@Component({
    selector: 'chat-bubble',
    templateUrl: './chat-bubble.widget.html',
    styleUrls: ['./chat-bubble.widget.scss']
})

export class ChatBubbleWidget {
    @Input() role!: "assistant" | "user"
    @Input() input!: string

    constructor() {}
}