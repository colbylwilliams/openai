//
//  Service.swift
//  OpenAI
//
//  Created by Colby L Williams on 1/24/23.
//

import Foundation
import Combine
import OpenAISwift

class ChatService : ObservableObject {
    var didChange = PassthroughSubject<Void, Never>()
    @Published var realTimeMessages: [Message] = DataSource.messages
    
    let openAI = OpenAISwift(authToken: "")
    
    func sendMessage(_ chatMessage: Message) {
        realTimeMessages.append(chatMessage)
        didChange.send(())
        
        switch chatMessage.messageKind {
        case .text(let message):
            realTimeMessages.append(Message(user: User.AI, messageKind: .loading))
            
            openAI.sendCompletion(with: message, maxTokens: 100) { result in // Result<OpenAI, OpenAIError>
                switch result {
                case .success(let success):
                    let text = success.choices.first?.text.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
                    DispatchQueue.main.async {
                        _ = self.realTimeMessages.popLast()
                        self.realTimeMessages.append(Message(user: User.AI, messageKind: .text(text)))
                        self.didChange.send(())
                    }
                case .failure(let failure):
                    print(failure.localizedDescription)
                }
            }
            
        default:
            fatalError("Unsuported message type")
        }
    }
}

struct DataSource {
    static let messages = [
        Message(user: User.Me, messageKind: .text("Hello")),
        Message(user: User.AI, messageKind: .text("Hi")),
        Message(user: User.Me, messageKind: .text("Hi, I really love your templates and I would like to buy the chat template")),
        Message(user: User.AI, messageKind: .text("Thanks, nice to hear that, can I have your email please?")),
        Message(user: User.Me, messageKind: .text("😇")),
        Message(user: User.Me, messageKind: .text("Oh actually, I have just purchased the chat template, so please check your email, you might see my order")),
        Message(user: User.AI, messageKind: .text("Great, wait me a sec, let me check")),
        Message(user: User.Me, messageKind: .text("Sure"))
    ]
}
