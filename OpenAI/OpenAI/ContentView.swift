//
//  ContentView.swift
//  OpenAI
//
//  Created by Colby L Williams on 1/24/23.
//

import SwiftUI
import OpenAISwift
import SwiftyChat

struct ContentView: View {
    
//    @State var messages: [MockMessages.ChatMessageItem] = MockMessages.generateMessage(kind: .Text, count: 20)
    @EnvironmentObject var chatService: ChatService
    
    // MARK: - InputBarView variables
    @State private var message = ""
    @State private var isEditing = false
    
    var body: some View {
        NavigationView {
            chatView
        }
    }
    
    private var chatView: some View {
//        ChatView<MockMessages.ChatMessageItem, MockMessages.ChatUserItem>(messages: $messages) {
        ChatView<Message, User>(messages: $chatService.realTimeMessages) {

            BasicInputView(
                message: $message,
                isEditing: $isEditing,
                placeholder: "Type something",
                onCommit: { messageKind in
                    chatService.sendMessage(Message(user: User.Me, messageKind: messageKind))
                }
            )
            .padding(8)
            .padding(.bottom, 20)
//            .padding(.bottom, isEditing ? 0 : 8)
            .animation(.linear, value: isEditing)
//            .accentColor(.chatBlue)
            .background(Color.primary.colorInvert())
            .embedInAnyView()
            
        }
        // ▼ Optional, Present context menu when cell long pressed
        .messageCellContextMenu { message -> AnyView in
            switch message.messageKind {
            case .text(let text):
                return Button(action: {
                    print("Copy Context Menu tapped!!")
                    UIPasteboard.general.string = text
                }) {
                    Text("Copy")
                    Image(systemName: "doc.on.doc")
                }.embedInAnyView()
            default:
                // If you don't want to implement contextMenu action
                // for a specific case, simply return EmptyView like below;
                return EmptyView().embedInAnyView()
            }
        }
        // ▼ Required
        .environmentObject(ChatMessageCellStyle.OpenAIStyle)
        .navigationBarTitle("OpenAI")
        .navigationBarTitleDisplayMode(.inline)
        .listStyle(PlainListStyle())
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(ChatService())
    }
}
